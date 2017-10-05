

help:  ## Show help for the available Make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

update-translations:  ## Rebuild translation files
	@./manage.py makemessages --keep-pot
	@sed -i 's/^"POT-Creation-Date:.*//' locale/django.pot
	@./manage.py compilemessages
