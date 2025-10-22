package org.example;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        final int puerto = 8080;

        try (ServerSocket serverSocket = new ServerSocket(puerto)) {
            System.out.println("Servidor iniciado. Esperando cliente en el puerto " + puerto + "...");

            Socket clientSocket = serverSocket.accept();
            System.out.println("Cliente conectado desde " + clientSocket.getInetAddress().getHostAddress() + "");

            DataInputStream input = new DataInputStream(clientSocket.getInputStream());
            DataOutputStream output = new DataOutputStream(clientSocket.getOutputStream());

            Thread threadEscuchar = new Thread(() -> {
                try {
                    while (true) {
                        String mensajeCliente = input.readUTF();
                        System.out.println("\nCliente dice: " + mensajeCliente);
                        System.out.print(">> Tú: ");
                    }
                } catch (IOException e) {
                    System.out.println("\nEl cliente se ha desconectado.");
                }
            });
            threadEscuchar.start();

            Scanner scanner = new Scanner(System.in);
            while (true) {
                System.out.print(">> Tú: ");
                String mensajeEnviar = scanner.nextLine();
                if ("salir".equalsIgnoreCase(mensajeEnviar)) {
                    break;
                }
                output.writeUTF(mensajeEnviar);
            }

            clientSocket.close();
            scanner.close();
            System.out.println("Servidor cerrado.");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}