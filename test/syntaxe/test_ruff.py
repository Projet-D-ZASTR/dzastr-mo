import subprocess


def test_ruff_check():
    result = subprocess.run(
        ["ruff", "check", ".", "--config", "pyproject.toml"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Ruff lint errors:\n{result.stdout}"


def test_ruff_format():
    result = subprocess.run(
        ["ruff", "format", "--check", ".", "--config", "pyproject.toml"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Ruff format errors:\n{result.stdout}"
