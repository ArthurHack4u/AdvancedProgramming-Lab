package org.example;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;

public class Cliente {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // datos de conexión INICIALES
        System.out.print("Introduce la IP del servidor (ej: localhost): ");
        String host = scanner.nextLine();

        System.out.print("Introduce el Puerto del servidor (ej: 8080): ");
        int puerto = 8080;
        try {
            String puertoInput = scanner.nextLine();
            
            if (!puertoInput.trim().isEmpty()) {
                puerto = Integer.parseInt(puertoInput);
            } else {
                System.out.println("Puerto vacío, usando puerto por defecto 8080.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Puerto inválido, usando puerto por defecto 8080.");
        }

        boolean appRunning = true;

        while (appRunning) {

            Socket socket = null;
            DataInputStream input = null;
            DataOutputStream output = null;
            Thread threadEscuchar = null;

            try {
                System.out.println("Conectando a " + host + ":" + puerto + "...");
                socket = new Socket(host, puerto);

                input = new DataInputStream(socket.getInputStream());
                output = new DataOutputStream(socket.getOutputStream());

                final DataInputStream finalInput = input;
                threadEscuchar = new Thread(() -> {
                    try {
                        while (true) {
                            String mensajeServidor = finalInput.readUTF();
                            System.out.print("\r" + mensajeServidor + "\n>> Tú: ");
                        }
                    } catch (IOException e) {
                        System.out.println("\n(Cambiando/Desconectando del chat)");
                    }
                });
                threadEscuchar.setDaemon(true);
                threadEscuchar.start();

                // envío de mensajes
                while (true) {
                    System.out.print(">> Tú: ");
                    String mensajeEnviar = scanner.nextLine();

                    if ("salir".equalsIgnoreCase(mensajeEnviar)) {
                        output.writeUTF(mensajeEnviar); 
                        appRunning = false; 
                        break;

                    } else if (mensajeEnviar.startsWith("/join")) { 
                        
                        String[] parts = mensajeEnviar.split(" ");
                        
                        if (parts.length < 3) {
                            System.out.println("--- Error: Uso incorrecto. ---");
                            System.out.println("--- El comando es: /join <host> <puerto> ---");
                        
                        } else {
                            // reintentar, intentar conexion
                            try {
                                String newHost = parts[1];
                                int newPort = Integer.parseInt(parts[2]);
                                
                                host = newHost;
                                puerto = newPort;
                                
                                System.out.println("Saltando a " + host + ":" + puerto + "...");
                                break;

                            } catch (NumberFormatException e) {
                                System.out.println("Error: El puerto '" + parts[2] + "' no es un número.");
                            } catch (Exception e) {
                                System.out.println("Error: Uso incorrecto. /join <host> <puerto>");
                            }
                        }

                    } else {
                        output.writeUTF(mensajeEnviar);
                    }
                }

            } catch (IOException e) {
                System.err.println("No se pudo conectar al servidor: " + e.getMessage());
                System.out.println("Reintentando en 5 segundos...");
                try {
                    Thread.sleep(5000);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                }
                
            } finally {
                System.out.println("Saliendo del chat...");
                try {
                    if (output != null) output.close();
                    if (input != null) input.close();
                    if (socket != null) socket.close();
                } catch (IOException e) {
                }
            }
        }

        scanner.close();
        System.out.println("Has salido del chat. Bye"); 
    }
}