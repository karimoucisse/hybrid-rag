from ingestion import file_loader
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def test():
#     return ("hello world !")

def main():
    try:
        text = file_loader('data/wars1.pdf')
        print(text)
    except ValueError as e:
        print(f"Error: {e}")

main()
