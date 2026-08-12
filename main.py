import json
import time
import re


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
# 행렬 출력
# --------------------------------------------------
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(value) for value in row))


# --------------------------------------------------
# MAC 연산
# --------------------------------------------------
def calculate_mac(pattern, filter_data):
    score = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_data[i][j]

    return score


# --------------------------------------------------
# 행렬 크기 검사
# --------------------------------------------------
def is_valid_matrix(matrix, size):
    if not isinstance(matrix, list):
        return False

    if len(matrix) != size:
        return False

    for row in matrix:
        if not isinstance(row, list):
            return False

        if len(row) != size:
            return False

    return True


# --------------------------------------------------
# 점수 비교 - A/B
# --------------------------------------------------
def compare_scores(score_a, score_b):
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"

    if score_a > score_b:
        return "A"

    return "B"


# --------------------------------------------------
# 점수 비교 - Cross/X
# --------------------------------------------------
def classify_pattern(cross_score, x_score):
    if abs(cross_score - x_score) < EPSILON:
        return "UNDECIDED"

    if cross_score > x_score:
        return "Cross"

    return "X"


# --------------------------------------------------
# 라벨 정규화
# --------------------------------------------------
def normalize_label(label):
    if not isinstance(label, str):
        return None

    label = label.strip().lower()

    if label in ["+", "cross"]:
        return "Cross"

    if label == "x":
        return "X"

    return None


# --------------------------------------------------
# 패턴 키에서 크기 N 추출
# 예: size_13_2 → 13
# --------------------------------------------------
def extract_size(pattern_key):
    match = re.match(r"size_(\d+)_\d+", pattern_key)

    if match is None:
        return None

    return int(match.group(1))


# --------------------------------------------------
# MAC 실행 시간 측정
# --------------------------------------------------
def measure_mac_time(pattern, filter_data, repeat=10):
    total_time = 0.0

    for _ in range(repeat):
        start_time = time.perf_counter()

        calculate_mac(pattern, filter_data)

        end_time = time.perf_counter()

        total_time += end_time - start_time

    average_time = total_time / repeat

    return average_time * 1000


# --------------------------------------------------
# 3x3 Cross 생성
# --------------------------------------------------
def create_cross_3():
    return [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]


# --------------------------------------------------
# 3x3 X 생성
# --------------------------------------------------
def create_x_3():
    return [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]


# --------------------------------------------------
# 성능 분석
# --------------------------------------------------
def performance_analysis(filters):
    print("\n#----------------------------------------")
    print("# 성능 분석 (평균/10회)")
    print("#----------------------------------------")

    results = []

    # 3x3
    cross_3 = create_cross_3()

    time_3 = measure_mac_time(
        cross_3,
        cross_3,
        10
    )

    results.append((3, time_3, 3 * 3))

    # data.json의 5, 13, 25 필터
    for size in [5, 13, 25]:
        size_key = f"size_{size}"

        if size_key not in filters:
            continue

        filter_group = filters[size_key]

        cross_filter = None

        for key, value in filter_group.items():
            if normalize_label(key) == "Cross":
                cross_filter = value
                break

        if cross_filter is None:
            continue

        if not is_valid_matrix(cross_filter, size):
            continue

        average_time = measure_mac_time(
            cross_filter,
            cross_filter,
            10
        )

        results.append(
            (
                size,
                average_time,
                size * size
            )
        )

    print()
    print(f"{'크기':<10}{'평균 시간(ms)':<20}{'연산 횟수'}")
    print("-" * 45)

    for size, average_time, operations in results:
        print(
            f"{size}x{size:<7}"
            f"{average_time:<20.6f}"
            f"{operations}"
        )


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

    result = compare_scores(
        score_a,
        score_b
    )

    average_time = measure_mac_time(
        pattern,
        filter_a,
        10
    )

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(
        f"연산 시간(평균/10회): "
        f"{average_time:.6f} ms"
    )

    if result == "UNDECIDED":
        print(
            "판정: 판정 불가 "
            f"(|A-B| < {EPSILON})"
        )
    else:
        print(f"판정: {result}")

    # 3x3 성능 표
    print("\n#----------------------------------------")
    print("# [4] 성능 분석")
    print("#----------------------------------------")

    print(
        f"크기: 3x3 | "
        f"평균 시간: {average_time:.6f} ms | "
        f"연산 횟수: 9"
    )


# --------------------------------------------------
# JSON 파일 읽기
# --------------------------------------------------
def load_json(filename="data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"오류: {filename} 파일을 찾을 수 없습니다.")
        return None

    except json.JSONDecodeError:
        print(f"오류: {filename}의 JSON 형식이 올바르지 않습니다.")
        return None


# --------------------------------------------------
# JSON 분석 모드
# --------------------------------------------------
def json_analysis_mode():
    data = load_json()

    if data is None:
        return

    filters = data.get("filters")
    patterns = data.get("patterns")

    if not isinstance(filters, dict):
        print("오류: filters 데이터가 없습니다.")
        return

    if not isinstance(patterns, dict):
        print("오류: patterns 데이터가 없습니다.")
        return

    print("\n#----------------------------------------")
    print("# [1] 필터 로드")
    print("#----------------------------------------")

    # 필터 로드 상태 출력
    for size in [5, 13, 25]:
        size_key = f"size_{size}"

        if size_key not in filters:
            print(f"✗ {size_key} 필터 없음")
            continue

        filter_group = filters[size_key]

        labels = []

        for filter_name in filter_group.keys():
            normalized = normalize_label(filter_name)

            if normalized is not None:
                labels.append(normalized)

        if "Cross" in labels and "X" in labels:
            print(
                f"✓ {size_key} 필터 로드 완료 "
                "(Cross, X)"
            )
        else:
            print(
                f"✗ {size_key} 필터 라벨 오류"
            )

    print("\n#----------------------------------------")
    print("# [2] 패턴 분석")
    print("#----------------------------------------")

    total_count = 0
    pass_count = 0
    fail_count = 0

    failed_cases = []

    # 모든 패턴 분석
    for pattern_key, pattern_info in patterns.items():
        total_count += 1

        print(f"\n--- {pattern_key} ---")

        # -------------------------------
        # 패턴 키에서 크기 추출
        # -------------------------------
        size = extract_size(pattern_key)

        if size is None:
            reason = "패턴 키 형식 오류"

            print(f"FAIL ({reason})")

            fail_count += 1
            failed_cases.append(
                (pattern_key, reason)
            )

            continue

        size_key = f"size_{size}"

        # -------------------------------
        # 해당 크기의 필터 존재 확인
        # -------------------------------
        if size_key not in filters:
            reason = f"{size_key} 필터 없음"

            print(f"FAIL ({reason})")

            fail_count += 1
            failed_cases.append(
                (pattern_key, reason)
            )

            continue

        filter_group = filters[size_key]

        # -------------------------------
        # Cross / X 필터 찾기
        # -------------------------------
        cross_filter = None
        x_filter = None

        for filter_name, filter_value in filter_group.items():
            normalized = normalize_label(filter_name)

            if normalized == "Cross":
                cross_filter = filter_value

            elif normalized == "X":
                x_filter = filter_value

        if cross_filter is None or x_filter is None:
            reason = "Cross 또는 X 필터 없음"

            print(f"FAIL ({reason})")

            fail_count += 1
            failed_cases.append(
                (pattern_key, reason)
            )

            continue

        # -------------------------------
        # input / expected 확인
        # -------------------------------
        if not isinstance(pattern_info, dict):
            reason = "패턴 데이터 형식 오류"

            print(f"FAIL ({reason})")

            fail_count += 1
            failed_cases.append(
                (pattern_key, reason)
            )

            continue

        pattern = pattern_info.get("input")
        expected_raw = pattern_info.get("expected")

        expected = normalize_label(expected_raw)

        if expected is None:
            reason = f"expected 라벨 오류: {expected_raw}"

            print(f"FAIL ({reason})")

            fail_count += 1
            failed_cases.append(
                (pattern_key, reason)
            )

            continue

        # -------------------------------
        # 크기 검증
        # -------------------------------
        if not is_valid_matrix(pattern, size):
            reason = "패턴 크기 불일치"

            print(f"FAIL ({reason})")

            fail_count += 1
            failed_cases.append(
                (pattern_key, reason)
            )

            continue

        if not is_valid_matrix(cross_filter, size):
            reason = "Cross 필터 크기 불일치"

            print(f"FAIL ({reason})")

            fail_count += 1
            failed_cases.append(
                (pattern_key, reason)
            )

            continue

        if not is_valid_matrix(x_filter, size):
            reason = "X 필터 크기 불일치"

            print(f"FAIL ({reason})")

            fail_count += 1
            failed_cases.append(
                (pattern_key, reason)
            )

            continue

        # -------------------------------
        # MAC 연산
        # -------------------------------
        cross_score = calculate_mac(
            pattern,
            cross_filter
        )

        x_score = calculate_mac(
            pattern,
            x_filter
        )

        result = classify_pattern(
            cross_score,
            x_score
        )

        print(f"Cross 점수: {cross_score}")
        print(f"X 점수: {x_score}")

        # -------------------------------
        # expected 비교
        # -------------------------------
        if result == expected:
            print(
                f"판정: {result} | "
                f"expected: {expected} | PASS"
            )

            pass_count += 1

        else:
            if result == "UNDECIDED":
                reason = "동점 규칙에 따라 UNDECIDED"
            else:
                reason = (
                    f"판정 {result}, "
                    f"expected {expected}"
                )

            print(
                f"판정: {result} | "
                f"expected: {expected} | FAIL"
            )

            fail_count += 1

            failed_cases.append(
                (pattern_key, reason)
            )

    # --------------------------------------------------
    # 성능 분석
    # --------------------------------------------------
    performance_analysis(filters)

    # --------------------------------------------------
    # 결과 요약
    # --------------------------------------------------
    print("\n#----------------------------------------")
    print("# [4] 결과 요약")
    print("#----------------------------------------")

    print(f"총 테스트: {total_count}개")
    print(f"통과: {pass_count}개")
    print(f"실패: {fail_count}개")

    if failed_cases:
        print("\n실패 케이스:")

        for case_name, reason in failed_cases:
            print(
                f"- {case_name}: {reason}"
            )

    else:
        print("\n모든 테스트를 통과했습니다.")


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
        json_analysis_mode()

    else:
        print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()