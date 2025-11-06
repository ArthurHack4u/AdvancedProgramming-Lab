package org.example;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.Scanner;

public class Servidor {

    private static final List<ClientHandler> clients = new CopyOnWriteArrayList<>();
    private static final int puertoDefault = 3030;
    // puerto defecto por si no se ingresa nada

    public static void main(String[] args) {

        int puerto = puertoDefault;

        Scanner scanner = new Scanner(System.in);
        System.out.print("Introduce el puerto para iniciar el servidor (puerto default 3030): ");

        try {
            String input = scanner.nextLine();
            
            if (!input.trim().isEmpty()) {
                puerto = Integer.parseInt(input);
            } else {
                System.out.println("No se ingresó puerto. Usando por defecto: " + puertoDefault);
            }
        } catch (NumberFormatException e) {
            System.err.println("Entrada inválida. Usando puerto por defecto: " + puertoDefault);
        }
        
        scanner.close(); 


        try (ServerSocket serverSocket = new ServerSocket(puerto)) {
            System.out.println("Servidor de chat iniciado en el puerto " + puerto + "...");

            // aceptar múltiples clientes
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Nuevo cliente conectado: " + clientSocket.getInetAddress().getHostAddress());

                ClientHandler clientHandler = new ClientHandler(clientSocket, clients);
                clients.add(clientHandler);
                new Thread(clientHandler).start();
            }

        } catch (IOException e) {
            System.err.println("No se pudo iniciar el servidor en el puerto " + puerto);
            e.printStackTrace();
        }
    }
}