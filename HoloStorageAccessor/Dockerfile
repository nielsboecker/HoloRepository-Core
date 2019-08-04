FROM golang:1.12.7 AS build
CMD mkdir /workspace
WORKDIR /workspace
COPY api ./api
COPY cmd ./cmd
COPY configs ./configs
COPY internal ./internal
COPY third_party ./third_party

ENV CGO_ENABLED=0
RUN go get -d -v ./...
RUN go build -a -installsuffix cgo -o holo-storage-accessor cmd/holo-storage-accessor/main.go

FROM scratch AS runtime
ENV GIN_MODE=release
COPY --from=build /workspace/third_party ./third_party
COPY --from=build /workspace/api ./api
COPY --from=build /workspace/configs ./configs
COPY --from=build /workspace/holo-storage-accessor ./
EXPOSE 8080/tcp
ENTRYPOINT ["./holo-storage-accessor"]
