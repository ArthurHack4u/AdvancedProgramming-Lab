package org.example;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class Servidor {

    private static List<ClientHandler> clients = new CopyOnWriteArrayList<>();

    public static void main(String[] args) {
        final int puerto = 8080;

        try (ServerSocket serverSocket = new ServerSocket(puerto)) {
            System.out.println("Servidor de chat iniciado en el puerto " + puerto + "...");

            // Bucle para aceptar múltiples clientes
            while (true) {
                // espera a que un cliente se conecte
                Socket clientSocket = serverSocket.accept();
                System.out.println("Nuevo cliente conectado: " + clientSocket.getInetAddress().getHostAddress());

                // manejador para este cliente
                ClientHandler clientHandler = new ClientHandler(clientSocket, clients);

                // agrega el manejador a la lista de clientes
                clients.add(clientHandler);

                // Inicia el hilo de escucha a este cliente
                new Thread(clientHandler).start();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

