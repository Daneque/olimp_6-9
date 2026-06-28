import sys
import subprocess
from pathlib import Path


TIMEOUT_SECONDS = 5



def natural_key(path: Path):
    name = path.name
    parts = []
    cur = ''
    is_digit = None
    for ch in name:
        if ch.isdigit():
            if is_digit is False:
                parts.append(cur)
                cur = ch
            else:
                cur += ch
            is_digit = True
        else:
            if is_digit is True:
                parts.append(int(cur))
                cur = ch
            else:
                cur += ch
            is_digit = False
    if cur:
        parts.append(int(cur) if is_digit else cur)
    return parts



def normalize_output(text: str) -> str:
    return ''.join(text.split())



def run_solution(solution_path: Path, input_text: str):
    try:
        result = subprocess.run(
            [sys.executable, solution_path.name],
            input=input_text,
            text=True,
            capture_output=True,
            timeout=TIMEOUT_SECONDS,
            cwd=solution_path.parent,
        )
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'timeout': False,
        }
    except subprocess.TimeoutExpired:
        return {
            'returncode': None,
            'stdout': '',
            'stderr': 'Time limit exceeded',
            'timeout': True,
        }



def collect_test_pairs(tests_dir: Path):
    pairs = []
    for in_file in sorted(tests_dir.glob('*.in'), key=natural_key):
        out_file = tests_dir / f'{in_file.stem}.out'
        if out_file.exists():
            pairs.append((in_file, out_file))
    return pairs



def check_task(task_dir: Path):
    solution_path = task_dir / 'solution.py'
    tests_dir = task_dir / 'tests'

    result = {
        'task_name': task_dir.name,
        'passed': 0,
        'failed': 0,
        'total': 0,
        'failures': [],
        'skipped_reason': None,
    }

    if not solution_path.exists():
        result['skipped_reason'] = 'нет solution.py'
        return result

    if not tests_dir.exists():
        result['skipped_reason'] = 'нет папки tests'
        return result

    pairs = collect_test_pairs(tests_dir)
    if not pairs:
        result['skipped_reason'] = 'нет пар .in/.out'
        return result

    print(f'\n=== {task_dir.name} ===')
    print(f'Найдено тестов: {len(pairs)}')

    for in_file, out_file in pairs:
        base = in_file.stem
        print(f'Checking test {base}')

        input_text = in_file.read_text(encoding='utf-8')
        expected_raw = out_file.read_text(encoding='utf-8')
        expected = normalize_output(expected_raw)

        run = run_solution(solution_path, input_text)
        result['total'] += 1

        if run['timeout']:
            print(f'  TIME LIMIT on test {base}')
            result['failed'] += 1
            result['failures'].append((base, 'TL'))
            continue

        if run['returncode'] != 0:
            print(f'  RUNTIME ERROR on test {base}')
            err = run['stderr'].strip()
            if err:
                print(f'  stderr: {err.splitlines()[0]}')
            result['failed'] += 1
            result['failures'].append((base, 'RE'))
            continue

        got = normalize_output(run['stdout'])

        if expected != got:
            print(f'  MISMATCH on test {base}')
            print(f'  expected: {expected}')
            print(f'  got     : {got}')
            result['failed'] += 1
            result['failures'].append((base, 'WA'))
        else:
            print(f'  OK test {base}')
            result['passed'] += 1

    return result



def main():
    root = Path('.')
    task_dirs = sorted(
        [p for p in root.iterdir() if p.is_dir() and p.name.startswith('task_')],
        key=natural_key,
    )

    if not task_dirs:
        print('Не найдены папки task_*')
        sys.exit(1)

    all_results = []
    total_passed = 0
    total_failed = 0
    total_tests = 0

    for task_dir in task_dirs:
        result = check_task(task_dir)
        all_results.append(result)
        total_passed += result['passed']
        total_failed += result['failed']
        total_tests += result['total']

        if result['skipped_reason']:
            print(f'\n=== {task_dir.name} ===')
            print(f'Пропущено: {result["skipped_reason"]}')

    print('\n=== СВОДКА ПО ЗАДАЧАМ ===')
    for result in all_results:
        if result['skipped_reason']:
            print(f'{result["task_name"]}: ПРОПУЩЕНО ({result["skipped_reason"]})')
        elif result['failed'] == 0:
            print(f'{result["task_name"]}: ПРОЙДЕНО {result["passed"]}/{result["total"]}')
        else:
            failed_list = ', '.join(f'{test} [{reason}]' for test, reason in result['failures'])
            print(f'{result["task_name"]}: НЕ ПРОЙДЕНО {result["passed"]}/{result["total"]}; ошибки: {failed_list}')

    print('\n=== ОБЩАЯ СВОДКА ===')
    print(f'Пройдено тестов : {total_passed}')
    print(f'Не пройдено     : {total_failed}')
    print(f'Всего тестов    : {total_tests}')


if __name__ == '__main__':
    main()
