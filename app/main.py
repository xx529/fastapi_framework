from app.apiserver import myapp

myapp = myapp

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app='main:myapp',
        host='localhost',
        port=8000,
        reload=True,
        app_dir='app',
        workers=5
    )
