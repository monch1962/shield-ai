# Build stage: static stdlib-only binaries (no external Go modules).
FROM golang:1.23-alpine AS build
WORKDIR /src
COPY go.mod ./
COPY *.go ./
COPY cmd/ ./cmd/
RUN go build -o /out/sidecar . && go build -o /out/mocktool ./cmd/mocktool

FROM alpine:3.20
COPY --from=build /out/sidecar /out/mocktool /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/sidecar"]
