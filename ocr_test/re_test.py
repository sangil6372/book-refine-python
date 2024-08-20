from hanspell import spell_checker
from hanspell.constants import CheckResult

print(CheckResult.PASSED)
print(CheckResult.WRONG_SPELLING)
print(CheckResult.WRONG_SPACING)
print(CheckResult.AMBIGUOUS)
print(CheckResult.STATISTICAL_CORRECTION)

text = "외않되"
spelled_text = spell_checker.check(text)
print(spelled_text)


checked_text = spelled_text.checked
print(checked_text)
