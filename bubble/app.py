from flask import Flask, request, jsonify
import os

app = Flask(__name__)


def bubble_sort_with_steps(arr):
   
    steps = []
    data = list(arr)
    n = len(data)
    
 
    steps.append({
        "array": list(data),
        "comparing": [],
        "sortedIndex": [],
        "message": "초기 데이터 배열 생성 완료"
    })

   
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
          
            steps.append({
                "array": list(data),
                "comparing": [j, j + 1],
                "sortedIndex": [n - 1 - k for k in range(i)],
                "message": f"{data[j]}와 {data[j+1]} 비교 중"
            })

            if data[j] > data[j + 1]:
                
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
                steps.append({
                    "array": list(data),
                    "comparing": [j, j + 1],
                    "sortedIndex": [n - 1 - k for k in range(i)],
                    "message": f"조건 충족으로 위치 교환: {data[j+1]} ↔ {data[j]}"
                })
        
       
        steps.append({
            "array": list(data),
            "comparing": [],
            "sortedIndex": [n - 1 - k for k in range(i + 1)],
            "message": f"뒤에서 {i+1}번째 원소 정렬 완료"
        })

       
        if not swapped and i == 0:
            steps.append({
                "array": list(data),
                "comparing": [],
                "sortedIndex": list(range(n)),
                "message": "배열이 이미 정렬되어 있어 조기 완료되었습니다 (최선 복잡도 O(n))"
            })
            break

    return steps, data

@app.route("/", methods=["POST", "GET"])
def handle_bubble_sort():
    
    if request.method == "GET":
        return jsonify({
            "status": "active",
            "message": "Google Cloud Run Bubble Sort API is running smoothly."
        }), 200

    try:
        req_data = request.get_json(silent=True) or {}
        numbers = req_data.get("numbers", [64, 34, 25, 12, 22, 11, 90])
        
     
        numbers = [int(x) for x in numbers]

        steps, sorted_result = bubble_sort_with_steps(numbers)

        return jsonify({
            "status": "success",
            "backend": "Google Cloud Run (Python Flask)",
            "steps": steps,
            "sorted": sorted_result,
            "complexity": {
                "time_best": "O(n)",
                "time_worst": "O(n^2)",
                "space": "O(1)"
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == "__main__":
  
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
