from flask import Flask, jsonify, request
import os

app = Flask(__name__)

def selection_sort_steps(arr):
    """
    단순 선택 정렬(Selection Sort)의 전체 과정을 단계별로 기록하여 반환합니다.
    매 단계에서의 배열 상태, 비교 중인 인덱스, 교환 여부 등을 포함합니다.
    """
    steps = []
    n = len(arr)
    
    # 초기 상태 기록
    steps.append({
        "step": 0,
        "array": list(arr),
        "comparing": [],
        "min_index": -1,
        "swapped": False,
        "description": "초기 배열 상태입니다."
    })
    
    for i in range(n - 1):
        min_idx = i
        # 최솟값 탐색 단계
        steps.append({
            "step": len(steps),
            "array": list(arr),
            "comparing": [i, min_idx],
            "min_index": min_idx,
            "swapped": False,
            "description": f"인덱스 {i}부터 시작하여 최솟값을 찾습니다. 현재 기준 최솟값 인덱스: {i} (값: {arr[i]})"
        })
        
        for j in range(i + 1, n):
            # 비교 수행
            steps.append({
                "step": len(steps),
                "array": list(arr),
                "comparing": [min_idx, j],
                "min_index": min_idx,
                "swapped": False,
                "description": f"인덱스 {j}의 값({arr[j]})과 현재 최솟값({arr[min_idx]})을 비교합니다."
            })
            
            if arr[j] < arr[min_idx]:
                min_idx = j
                steps.append({
                    "step": len(steps),
                    "array": list(arr),
                    "comparing": [min_idx],
                    "min_index": min_idx,
                    "swapped": False,
                    "description": f"더 작은 값 발견! 새로운 최솟값 인덱스: {min_idx} (값: {arr[min_idx]})"
                })
        
        # 최솟값과 현재 위치(i)의 원소 교환 (필요한 경우)
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append({
                "step": len(steps),
                "array": list(arr),
                "comparing": [i, min_idx],
                "min_index": min_idx,
                "swapped": True,
                "description": f"인덱스 {i}와 최솟값 인덱스 {min_idx}의 위치를 서로 교환합니다."
            })
        else:
            steps.append({
                "step": len(steps),
                "array": list(arr),
                "comparing": [i],
                "min_index": min_idx,
                "swapped": False,
                "description": f"인덱스 {i}는 이미 올바른 위치에 있습니다. 교환을 생략합니다."
            })
            
    # 최종 완료 상태 기록
    steps.append({
        "step": len(steps),
        "array": list(arr),
        "comparing": [],
        "min_index": -1,
        "swapped": False,
        "description": "선택 정렬이 완전히 완료되었습니다!"
    })
    
    return steps

@app.route('/sort', methods=['POST'])
def sort_endpoint():
    """
    클라이언트로부터 배열 데이터를 받아 선택 정렬 단계를 계산하여 반환합니다.
    """
    try:
        data = request.get_json()
        if not data or 'array' not in data:
            return jsonify({"error": "Invalid input, 'array' field is required."}), 400
        
        input_array = data['array']
        if not isinstance(input_array, list) or not all(isinstance(x, (int, float)) for x in input_array):
            return jsonify({"error": "Array must contain numbers only."}), 400
            
        # 선택 정렬 단계 생성
        steps = selection_sort_steps(input_array)
        
        return jsonify({
            "status": "success",
            "algorithm": "Selection Sort",
            "time_complexity": "O(N^2)",
            "space_complexity": "O(1)",
            "total_steps": len(steps),
            "steps": steps
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "Cloud Run Selection Sort Backend"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
