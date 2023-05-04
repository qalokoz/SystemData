public class Main {
    public static void main(String[] args) {
      String serverName = "enter your server name here!";
      String dockerfile = generateDockerfile(serverName);
      System.out.println(dockerfile);
    }
  
    public static String generateDockerfile(String serverName) {
      String dockerfile = "FROM ubuntu:latest\n" +
                         "RUN apt-get update && apt-get install -y curl\n" +
                         "CMD curl " + serverName + " > index.html && python3 -m http.server";
      return dockerfile;
    }
  }