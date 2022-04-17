import concurrent.futures

from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['POST'])
def save():
    myFile = open("data", 'a+')
    data = request.get_json()
    sum = 0
    count = 0
    def additional_work():
        computation_overhead = 5**100000
        print(computation_overhead)

    for points in data:
        for point in points:
            values = point.split(",")
            if len(values)>17:
                try:
                    sum += float(values[9])
                except Exception as e:
                    try:
                        sum += int(values[9])
                    except Exception as e:
                        print(f"{values[9]} is not numeric value")
                count += 1
    res = 0 if count == 0 else sum/count
    additional_work()
    myFile.write(str(res))
    myFile.close()
    return "{'success':'true'}"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)