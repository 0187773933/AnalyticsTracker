package main

import (
	"os"
	"os/signal"
	"syscall"
	"fmt"
	"path/filepath"
	fiber "github.com/gofiber/fiber/v2"
	server "analyticstracker/v1/server"
	utils "analyticstracker/v1/utils"
)

var s *fiber.App

func SetupCloseHandler() {
	c := make( chan os.Signal )
	signal.Notify( c , os.Interrupt , syscall.SIGTERM , syscall.SIGINT )
	go func() {
		<-c
		fmt.Println( "\r- Ctrl+C pressed in Terminal" )
		fmt.Println( "Shutting Down AnalyticsTracker Server" )
		s.Shutdown()
		os.Exit( 0 )
	}()
}

func main() {
	SetupCloseHandler()
	config_file_path , _ := filepath.Abs( os.Args[ 1 ] )
	// config_file_path := "/app/config.json"
	fmt.Println( config_file_path )
	config := utils.ParseConfig( config_file_path )
	fmt.Println( config )
	s = server.New( config )
	fmt.Printf( "Listening on %s\n" , config.ServerPort )
	result := s.Listen( fmt.Sprintf( ":%s" , config.ServerPort ) )
	fmt.Println( result )
}