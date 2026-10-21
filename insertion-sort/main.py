# main.py
from flask import Flask, jsonify, request

app = Flask(__name__)


def insertion_sort_steps(arr):
  """단순 삽입 정렬(Straight Insertion Sort)을 수행하고 각 단계별 배열 상태를 기록하는 함수.

  정렬 과정의 모든 단계를 리스트로 반환하여 클라이언트에서 시각화할 수 있도록 합니다.

  Args:
      arr (list): 정렬할 정수 리스트

  Returns:
      list: 각 단계별 배열 상태를 담은 2차원 리스트
  """
  steps = []
  n = len(arr)
  # 원본 배열의 초기 상태 추가
  steps.append(list(arr))

  for i in range(1, n):
    key = arr[i]
    j = i - 1
    # 현재 원소(key)를 정렬된 앞쪽 영역의 적절한 위치에 삽입
    while j >= 0 and arr[j] > key:
      arr[j + 1] = arr[j]
      j -= 1
    arr[j + 1] = key
    # 각 정렬 단계 완료 후의 배열 상태 저장
    steps.append(list(arr))

  return steps


@app.route('/sort', methods=['POST'])
def sort_endpoint():
  """클라이언트로부터 정렬할 배열 데이터를 받아 단순 삽입 정렬을 수행한 후,

  단계별 결과와 시간/공간 복잡도 정보를 반환하는 API 엔드포인트.
  """
  try:
    data = request.get_json()
    if not data or 'array' not in data:
      return (
          jsonify({
              'error': (
                  "잘못된 요청입니다. 'array' 필드에 정수 리스트를 전달해주세요."
              )
          }),
          400,
      )

    input_array = data['array']
    if not isinstance(input_array, list) or not all(
        isinstance(x, int) for x in input_array
    ):
      return (
          jsonify({
              'error': (
                  '배열의 모든 원소는 정수(int) 타입이어야 합니다.'
              )
          }),
          400,
      )

    # 단순 삽입 정렬 수행 및 단계별 기록 생성
    sorting_steps = insertion_sort_steps(list(input_array))

    # 응답 데이터 구성
    response_data = {
        'status': 'success',
        'input_array': input_array,
        'sorted_array': sorting_steps[-1] if sorting_steps else input_array,
        'steps': sorting_steps,
        'complexity': {
            'time_worst': 'O(n^2)',
            'time_average': 'O(n^2)',
            'time_best': 'O(n)',
            'space': 'O(1)',
        },
    }

    return jsonify(response_data), 200

  except Exception as e:
    return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
  """Cloud Run 서비스 상태 확인용 헬스체크 엔드포인트."""
  return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
  # 로컬 테스트 실행 설정
  app.run(host='0.0.0.0', port=8080, debug=True)
