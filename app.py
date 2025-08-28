from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import os
import gradio as gr
from load_models import agent
import numpy as np

# Globale Variable für die Ausgabe der Rezeptanleitung
agent_output = None

def create_recipe(rezept_zutaten, video_transkript):
    """
    Erstellt eine Rezeptanleitung basierend auf den Zutaten und dem Video-Transkript.
    """
    global agent_output
    try:
        if not rezept_zutaten or not video_transkript:
            raise ValueError("Zutaten und Video-Transkript müssen vorhanden sein.")

        result_sync = agent.run_sync(
            f"Erstelle mir einen Schritt-für-Schritt-Guide für die {rezept_zutaten} basierend auf den {video_transkript} und benutze alle Informationen genau."
            f"Starte mit: *Hier ist ein Schritt-für-Schritt-Guide für (denke Rezeptnamen aus)*:"
            f"Dann: *Zutaten:*"
            f"Dann: *Schritt-für-Schritt-Anleitung:*"
            f"Achte darauf, dass es nicht zu viele Schritte (1-10)."
            f"Gebe Empfehlungen zum Schluss, was man alles vorher machen kann, wie z.B. *Empfehlungen:* Gemüse vorschneiden oder Fleisch marinieren."
            f"Weitere Empfehlungen können auch mögliche Zeitersparnisse durch parallele Zubereitung von Komponenten sein."
        )
        agent_output = result_sync.output
        return result_sync.output
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {repr(e)}"

def generate_audio(steps_output):
    """
    Generiert eine Audio-Datei basierend auf dem Text der Erklärung mit Kokoro (nur auf englisch).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "kokoro.wav")

    pipeline = KPipeline(lang_code='a')
    text = steps_output

    generator = pipeline(
        text, 
        voice='af_heart', 
        speed=1, 
        split_pattern=r'\n+'
    )

    audio_data = []
    sampling_rate = 24000

    for i, (gs, ps, audio) in enumerate(generator):
        audio_data.append(audio)

    combined_audio = np.concatenate(audio_data)
    sf.write(output_path, combined_audio, sampling_rate)

    return output_path

def explain_steps(step_nummer: int, question_input: str | None):
    """
    Erklärt einen bestimmten Schritt der Rezeptanleitung.
    """
    if agent_output is None:
        return "Bitte erstellen Sie zuerst die Rezeptanleitung", None

    try:
        anfrage = (
            f"Du bist ein erfahrener Kochassistent."
            f"Erkläre nur Schritt {step_nummer} basierend auf {agent_output}."
            f"Die Erklärung muss auf Englisch sein."
            f"{' und der Frage ' + question_input if question_input else ''}. "
            f"Wenn Schritt {step_nummer} nicht vorhanden ist, schreibe 'Versuche einen anderen Schritt'."
            f"Wenn Schritt {step_nummer} der letzte Schritt ist, gebe die Anweisung und schreibe dazu"
            f"Das war der letzte Schritt. Guten Appetit!"
            f"Beantworte keine Frage, wenn es nicht um das Rezept oder Kochen im Allgemeinen geht."
        )
        result_step = agent.run_sync(anfrage)
        steps_output = result_step.output

        audio_path = generate_audio(steps_output)
        return steps_output, audio_path
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}", None
    
def clear_recipe_fields():
    return "", "", ""  

# Laden von Beispielen
script_dir = os.path.dirname(__file__)
transcript_path = os.path.join(script_dir, 'transkript.txt')
ingredients_path = os.path.join(script_dir, 'zutaten.txt')

with open(transcript_path, 'r', encoding='utf-8') as f:
    transcript_text = f.read()

with open(ingredients_path, 'r', encoding='utf-8') as f:
    ingredients_text = f.read()

# Erstellung des Gradio-Interfaces
with gr.Blocks() as demo:
    gr.Markdown("# Rezept Anleitung Generator")

    with gr.Tab("Rezept Anleitung erstellen"):
        recipe_input = gr.Textbox(label="Rezept Zutaten", value=ingredients_text)
        video_transcript = gr.Textbox(label="Video Transkript", lines=10, value=transcript_text)
        create_button = gr.Button("Rezept Erstellen")
        recipe_output = gr.Textbox(label="Rezept Anleitung")
        create_button.click(
            create_recipe,
            inputs=[recipe_input, video_transcript],
            outputs=recipe_output,
        )
        # Clear Button
        gr.Markdown(
            """
            **Hinweis:**  
            - Lösche die Beispieltexte (Clear Button) und füge dein eigenes Rezept und Transkript hinzu.  
            - Wechsle auf den zweiten Tab, um einzelne Schritte erklären zu lassen oder gezielte Fragen zum Rezept an den Agenten zu stellen.  
            - Die Antworten des Agenten werden auf Englisch ausgegeben und zusätzlich als Audio bereitgestellt.
            """
        )
        clear_button = gr.Button("Clear")

        clear_button.click(
            clear_recipe_fields,
            inputs=[],
            outputs=[recipe_input, video_transcript, recipe_output]
        )
    with gr.Tab("Schritt erklären auf Englisch (mit Audio)"):
        recipe_output2 = gr.Textbox(label="Rezept Anleitung", value=agent_output)
        update_button = gr.Button("Rezept anzeigen")  # Neuer Button, um Textfeld zu aktualisieren
        step_nummer_input = gr.Number(label="Schritt-Nummer")
        question_input = gr.Textbox(label="Stelle eigene Fragen zu einem Schritt")
        explain_button = gr.Button("Erklären")
        steps_output = gr.Textbox(label="Erklärung für Schritt (Englisch)")
        audio_output = gr.Audio(label="Audio-Erklärung")

        # Button, um das Textfeld mit agent_output zu füllen
        def update_recipe_output():
            return agent_output or "Bitte zuerst die Rezeptanleitung erstellen."

        update_button.click(
            update_recipe_output,
            inputs=[],
            outputs=recipe_output2
        )

        # Button, um Schritt zu erklären
        explain_button.click(
            explain_steps,
            inputs=[step_nummer_input, question_input],
            outputs=[steps_output, audio_output],
        )

if __name__ == "__main__":
    demo.launch()
