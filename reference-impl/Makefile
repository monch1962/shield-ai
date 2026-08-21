.PHONY: build test e2e bundle compose-up compose-down clean

build:
	cd sidecar && go build -o bin/sidecar . && go build -o bin/mocktool ./cmd/mocktool

test:
	cd sidecar && go test ./...

bundle:
	bash opa/build-bundle.sh

e2e: build
	bash scripts/e2e.sh

compose-up:
	docker compose up -d --build

compose-down:
	docker compose down

clean:
	rm -rf sidecar/bin opa/bundle.tar.gz
