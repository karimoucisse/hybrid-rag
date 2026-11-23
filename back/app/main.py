from app.ingestion import ingest_file
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def test():
#     return ("hello world !")

def main():
    try:
        text = ingest_file('data/wars1.pdf')
        # print(text)
    except ValueError as e:
        print(f"Error: {e}")

main()
