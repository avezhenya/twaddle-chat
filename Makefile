.PHONY: deploy_prod

deploy_prod:
	ssh chat.prod "cd /home/twaddle-chat/; \
	              git pull origin master; \
	              docker-compose stop; \
	              docker-compose rm; \
	              docker-compose build; \
	              docker-compose up -d;"
	@echo "Production is done!"