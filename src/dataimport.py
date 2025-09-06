import io

from urllib import request



def main(url):
    df = None
    with request.urlopen(url) as response, io.StringIO() as buffer:
        buffer.write(response.read().decode("utf-8"))
        buffer.seek(0)
        print(buffer.getvalue())


main(
    "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv"
)
