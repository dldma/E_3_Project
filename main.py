import time


EPSILON = 1e-9


# --------------------------------------------------
# N x N 행렬 입력
# --------------------------------------------------
def input_matrix(name, size=3):
    matrix = []

    print(f"\n{name} ({size}줄 입력, 공백 구분)")

    while len(matrix) < size:
        row_number = len(matrix) + 1
        user_input = input(f"{row_number}행: ")

        try:
            row = list(map(float, user_input.split()))

            if len(row) != size:
                print(
                    f"입력 형식 오류: 각 줄에 {size}개의 숫자를 "
                    "공백으로 구분해 입력하세요."
                )
                continue

            matrix.append(row)

        except ValueError:
            print("입력 형식 오류: 숫자만 입력하세요.")

    return matrix


# --------------------------------------------------
# 입력한 행렬 출력
# --------------------------------------------------
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(value) for value in row))


# --------------------------------------------------
# MAC 연산
# pattern과 filter의 같은 위치 값을 곱해서 모두 더함
# --------------------------------------------------
def calculate_mac(pattern, filter_data):
    score = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_data[i][j]

    return score


# --------------------------------------------------
# 두 점수 비교
# --------------------------------------------------
def compare_scores(score_a, score_b):
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"

    if score_a > score_b:
        return "A"

    return "B"


# --------------------------------------------------
# MAC 연산 시간 측정
# 필터 A와 B의 MAC 연산을 10회 반복
# --------------------------------------------------
def measure_mac_time(pattern, filter_a, filter_b, repeat=10):
    total_time = 0.0

    for _ in range(repeat):
        start_time = time.perf_counter()

        calculate_mac(pattern, filter_a)
        calculate_mac(pattern, filter_b)

        end_time = time.perf_counter()

        total_time += end_time - start_time

    average_time = total_time / repeat

    # 초 → 밀리초(ms)
    return average_time * 1000


# --------------------------------------------------
# 모드 1 : 사용자 입력
# --------------------------------------------------
def user_input_mode():
    print("\n#----------------------------------------")
    print("# [1] 필터 입력")
    print("#----------------------------------------")

    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")

    print("\n[저장된 필터 A]")
    print_matrix(filter_a)

    print("\n[저장된 필터 B]")
    print_matrix(filter_b)

    print("\n#----------------------------------------")
    print("# [2] 패턴 입력")
    print("#----------------------------------------")

    pattern = input_matrix("패턴")

    print("\n[저장된 패턴]")
    print_matrix(pattern)

    print("\n#----------------------------------------")
    print("# [3] MAC 결과")
    print("#----------------------------------------")

    score_a = calculate_mac(pattern, filter_a)
    score_b = calculate_mac(pattern, filter_b)

    result = compare_scores(score_a, score_b)

    average_time = measure_mac_time(
        pattern,
        filter_a,
        filter_b,
        repeat=10
    )

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {average_time:.6f} ms")

    if result == "UNDECIDED":
        print(
            f"판정: 판정 불가 "
            f"(|A-B| < {EPSILON})"
        )
    else:
        print(f"판정: {result}")


# --------------------------------------------------
# 메인
# --------------------------------------------------
def main():
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    choice = input("선택: ")

    if choice == "1":
        user_input_mode()

    elif choice == "2":
        print("\ndata.json 분석 모드는 다음 단계에서 구현합니다.")

    else:
        print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()