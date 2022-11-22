package utils

import (
	// "os"
	"fmt"
	"io/ioutil"
	"encoding/json"
	// "path/filepath"
	// "strconv"
	// "context"
	// "time"
	// "strings"
	// redis_lib "github.com/go-redis/redis/v7"
	// redis "github.com/0187773933/RedisManagerUtils/manager"
	types "analyticstracker/v1/types"
)

func ParseConfig( file_path string ) ( result types.ConfigFile ) {
	file_data , _ := ioutil.ReadFile( file_path )
	err := json.Unmarshal( file_data , &result )
	if err != nil { fmt.Println( err ) }
	return
}