# scripts/check_ollama.py
import ollama
import sys

def check_ollama():
    try:
        print("Checking Ollama conection...")
        
        # Check conections
        response = ollama.chat(
            model='llama2:7b',
            messages=[{'role': 'user', 'content': 'Hola'}]
        )
        
        print("Ollama is running")
        print(f"Response: {response['message']['content'][:50]}...")
        
        # Available models
        print("\n📦 Models :")
        models = ollama.list()
        for model in models['models']:
            print(f"  - {model['name']} (Tamaño: {model.get('size', 'N/A')})")
        
        return True
        
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        print("\nSolution:")
        print("1. Ensure Ollama is installed: https://ollama.com/")
        print("2. Run: ollama serve (in another terminal)")
        print("3. Download a model: ollama pull llama3.2")
        return False

if __name__ == "__main__":
    check_ollama()