import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # GAS 및 웹 클라이언트와의 통신을 위한 CORS 허용

# 단순 선택 정렬 알고리즘 구현 함수
def selection_sort(arr):
    """
    주어진 배열을 단순 선택 정렬(Selection Sort) 방식으로 정렬하고,
    각 단계별(Step-by-step) 배열의 상태를 리스트로 반환합니다.
    시간 복잡도: 최악, 평균, 최선 모두 O(n^2)
    """
    n = len(arr)
    steps = []
    
    # 복사본 생성 (원본 보호)
    current_arr = list(arr)
    
    for i in range(n - 1):
        min_index = i
        # 최솟값을 가진 인덱스 탐색
        for j in range(i + 1, n):
            if current_arr[j] < current_arr[min_index]:
                min_index = j
        
        # 최솟값과 현재 위치의 값을 교환 (Swap)
        if min_index != i:
            current_arr[i], current_arr[min_index] = current_arr[min_index], current_arr[i]
            
        # 현재 단계의 배열 상태를 기록
        steps.append({
            "step": i + 1,
            "array": list(current_arr),
            "swapped_indices": [i, min_index]
        })
        
    return steps

@app.route('/', methods=['GET'])
def health_check():
    """서버 동작 상태 확인용 엔드포인트"""
    return jsonify({
        "status": "정상 동작 중 (Running)",
        "service": "Google Cloud Run Python Server",
        "algorithm": "단순 선택 정렬 (Selection Sort)"
    }), 200

@app.route('/sort', methods=['POST'])
def run_sort():
    """클라이언트로부터 배열을 받아 정렬을 수행하고 단계별 결과를 반환"""
    try:
        data = request.get_json()
        raw_array = data.get("array", [64, 25, 12, 22, 11])
        
        # 선택 정렬 실행 및 단계별 결과 수집
        sorting_steps = selection_sort(raw_array)
        
        return jsonify({
            "success": True,
            "time_complexity": "O(n^2)",
            "space_complexity": "O(1)",
            "initial_array": raw_array,
            "total_steps": len(sorting_steps),
            "steps": sorting_steps
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    # Cloud Run 환경 변수 PORT를 사용하거나 기본값 8080 사용
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
