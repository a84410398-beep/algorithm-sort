from flask import Flask, request, jsonify

app = Flask(__name__)

def selection_sort_steps(arr):
    """
    단순 선택 정렬 알고리즘 (Simple Selection Sort)
    매 단계에서 가장 작은 값을 찾아 올바른 위치와 교환합니다.
    클라이언트에서 단계별 시각화를 할 수 있도록 모든 과정을 기록하여 반환합니다.
    """
    n = len(arr)
    steps = []
    # 초기 상태 기록
    steps.append({
        "array": list(arr),
        "currentIndex": -1,
        "minIndex": -1,
        "description": "초기 배열 상태"
    })
    
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            # 현재 탐색 중인 구간에서 최소값 인덱스 찾기
            steps.append({
                "array": list(arr),
                "currentIndex": j,
                "minIndex": min_idx,
                "description": f"인덱스 {j}와 현재 최소값 후보인덱스 {min_idx} 비교"
            })
            if arr[j] < arr[min_idx]:
                min_idx = j
                
        # 최소값을 현재 위치(i)와 교환
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append({
                "array": list(arr),
                "currentIndex": i,
                "minIndex": min_idx,
                "description": f"최소값 발견: 인덱스 {min_idx}의 값과 인덱스 {i}의 값 교환"
            })
        else:
            steps.append({
                "array": list(arr),
                "currentIndex": i,
                "minIndex": min_idx,
                "description": f"인덱스 {i}는 이미 제자리에 있습니다."
            })
            
    # 최종 완료 상태
    steps.append({
        "array": list(arr),
        "currentIndex": -1,
        "minIndex": -1,
        "description": "정렬 완료!"
    })
    return steps

@app.route('/sort', methods=['POST'])
def sort_endpoint():
    data = request.get_json() or {}
    arr = data.get('array', [64, 25, 12, 22, 11])
    
    # 선택 정렬 단계 생성
    steps = selection_sort_steps(arr)
    
    # 알고리즘 복잡도 정보 포함
    complexity = {
        "time_complexity": "O(n^2)",
        "space_complexity": "O(1)",
        "description": "단순 선택 정렬은 전체 구간에서 최소값을 찾아 선택하여 정렬하는 알고리즘입니다."
    }
    
    return jsonify({
        "status": "success",
        "steps": steps,
        "complexity": complexity
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "server": "Cloud Run Python Backend"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
