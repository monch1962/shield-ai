# Build context is the repo root (needed to reach policies/).
FROM openpolicyagent/opa:1.1.0 AS bundle
COPY policies/ /policies/
RUN mkdir /stage && cp /policies/*.rego /stage/ \
    && opa build -b /stage -o /bundle.tar.gz

FROM openpolicyagent/opa:1.1.0
COPY --from=bundle /bundle.tar.gz /bundle.tar.gz
COPY reference-impl/opa/config.yaml /config.yaml
CMD ["run", "--server", "--bundle", "/bundle.tar.gz", \
     "--config-file", "/config.yaml", "--addr", "0.0.0.0:8181"]
