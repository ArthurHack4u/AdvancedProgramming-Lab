package org.example;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;

public class Cliente {
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);

        System.out.print("Introduce la IP del servidor (ej: localhost o 127.0.0.1): ");
        String host = scanner.nextLine();
        
        System.out.print("Introduce el Puerto del servidor (ej: 8080): ");
        int puerto = 8080;
        try {
            puerto = Integer.parseInt(scanner.nextLine());
        } catch (NumberFormatException e) {
            System.out.println("Puerto inválido, usando puerto por defecto 8080.");
        }


        try (Socket socket = new Socket(host, puerto)) {
            System.out.println("Conectado al servidor en " + host + ":" + puerto);

            DataInputStream input = new DataInputStream(socket.getInputStream());
            DataOutputStream output = new DataOutputStream(socket.getOutputStream());

            // escuchar mensajes del servidor
            Thread threadEscuchar = new Thread(() -> {
                try {
                    while (true) {
                        String mensajeServidor = input.readUTF();
                        System.out.print("\r" + mensajeServidor + "\n>> Tú: ");
                    }
                } catch (IOException e) {
                    System.out.println("\nEl servidor se ha desconectado. Presiona Enter para salir.");
                }
            });
            threadEscuchar.setDaemon(true);
            threadEscuchar.start();

            // enviar mensajes
            while (true) {
                System.out.print(">> Tú: ");
                String mensajeEnviar = scanner.nextLine();

                output.writeUTF(mensajeEnviar);

                if ("salir".equalsIgnoreCase(mensajeEnviar)) {
                    break;
                }
            }

        } catch (IOException e) {
            System.err.println("No se pudo conectar al servidor: " + e.getMessage());
        }
    }
}