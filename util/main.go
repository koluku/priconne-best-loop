package main

import (
	"fmt"

	"github.com/atotto/clipboard"
	uuid "github.com/satori/go.uuid"
)

// id生成器
func main() {

	newID := uuid.NewV4()

	clipboard.WriteAll(newID.String())
	fmt.Println(newID.String())
}
