package main

import (
    "net/http"
    "log"

    "app/handlers"
)

func main() {
    http.HandleFunc("/", handlers.HomeHandler)
    
    log.Fatal(http.ListenAndServe(":9999", nil))
}
