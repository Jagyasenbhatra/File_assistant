import gradio as gr
import google.generativeai as genai
import os


genai.configure(api_key=os.environ.get('api_key'))


model = genai.GenerativeModel(model_name="gemini-pro")


def generate_response(user_input, file_path):
    """Generates a response using the Gemini model and file content."""
    try:

        try:
            with open(file_path.name, 'r', encoding='utf-8') as file:
                file_content = file.read()
        except UnicodeDecodeError:
            with open(file_path.name, 'r') as f:
                file_content = f.read()

        prompt = f"Based on the following information:\n{file_content}\n\nAnswer this question: {user_input}"

        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Error: Could not process the file or generate a response. {e}"


iface = gr.Interface(
    fn=generate_response,
    inputs=[
        gr.Textbox(lines=2, placeholder="Ask a question about the file..."),
        gr.File(type="filepath")
    ],
    outputs="text",
    title="File Q&A with Gemini",
    description="Upload a text file and ask questions about its content.",
)

iface.launch(share=True)
