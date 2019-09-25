package main

import (
	"database/sql"
	"log"
	"reflect"

	_ "github.com/go-sql-driver/mysql"
)

func main() {
	db, err := sql.Open("mysql", "lcark:test@tcp(127.0.0.1:3306)/test")
	if err != nil {
		log.Println(err)
	}
	rows, err := db.Query("select *  from test")
	if err != nil {
		log.Println(err)
	}
	log.Println(reflect.ValueOf(rows))
}
