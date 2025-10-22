package org.example;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;

public class Cliente {
    public static void main(String[] args) {
        final int puerto = 8080;
        final String host = "10.80.18.55";

        try (Socket socket = new Socket(host, puerto)) {
            System.out.println("Conectado al servidor en " + host + ":" + puerto);

            DataInputStream input = new DataInputStream(socket.getInputStream());
            DataOutputStream output = new DataOutputStream(socket.getOutputStream());

            Thread threadEscuchar = new Thread(() -> {
                try {
                    while (true) {
                        String mensajeServidor = input.readUTF();
                        System.out.println("\nServidor dice: " + mensajeServidor);
                        System.out.print(">> Tú: ");
                    }
                } catch (IOException e) {
                    System.out.println("\nEl servidor se ha desconectado.");
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

            /*
            scanner.close();
            System.out.println("Desconectado del servidor.");
            */


        } catch (IOException e) {
            System.err.println("No se pudo conectar al servidor: " + e.getMessage());
        }
    }
}