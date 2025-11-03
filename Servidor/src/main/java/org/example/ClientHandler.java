package org.example;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.List;

public class ClientHandler implements Runnable {

    private Socket clientSocket;
    private DataInputStream input;
    private DataOutputStream output;
    private String username;
    private List<ClientHandler> clients;

    public ClientHandler(Socket socket, List<ClientHandler> clients) throws IOException {
        this.clientSocket = socket;
        this.clients = clients;
        this.input = new DataInputStream(socket.getInputStream());
        this.output = new DataOutputStream(socket.getOutputStream());

        // nombre de usuario temporal
        this.username = "User-" + (clients.size() + 1);

        sendMessage("¡Conectado! Eres: " + this.username);
        sendMessage("Comandos disponibles: /nick <nuevo_nombre> | /pm <usuario> <mensaje>");
        broadcastMessage(this.username + " se ha unido al chat.", this);
    }

    @Override
    public void run() {
        try {
            while (true) {
                String mensajeCliente = input.readUTF();

                if (mensajeCliente.startsWith("/nick ")) {
                    // cambiar user
                    changeUserName(mensajeCliente);

                } else if (mensajeCliente.startsWith("/pm ")) {
                    // mensaje privado
                    sendPrivateMessage(mensajeCliente);

                } else if ("salir".equalsIgnoreCase(mensajeCliente)) {
                    break;

                } else {
                    // mensaje global
                    broadcastMessage(this.username + ": " + mensajeCliente, null);
                }
            }
        } catch (IOException e) {
            System.out.println(this.username + " se ha desconectado.");
        } finally {
            clients.remove(this);
            broadcastMessage(this.username + " ha salido del chat.", this);
            try {
                clientSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void changeUserName(String command) throws IOException {
        // Extrae el nuevo nombre del comando (ej: "/nick Arturo" -> "Arturo")
        String newNick = command.substring(6).trim();
        if (newNick.isEmpty()) {
            sendMessage("Error: El nombre no puede estar vacío.");
            return;
        }

        String oldNick = this.username;
        this.username = newNick;

        sendMessage("Tu nombre ha sido cambiado a: " + this.username);
        broadcastMessage(oldNick + " ahora es conocido como " + this.username, this);
    }

    private void sendPrivateMessage(String command) throws IOException {
        // Divide el comando: /pm <usuario> <mensaje>
        String[] parts = command.split(" ", 3);

        if (parts.length < 3) {
            sendMessage("Error: Uso incorrecto. /pm <usuario> <mensaje>");
            return;
        }

        String targetUser = parts[1];
        String message = parts[2];

        // Buscar al usuario en la lista de clientes
        for (ClientHandler client : clients) {
            if (client.username.equals(targetUser)) {
                // Encontrado: enviar mensaje privado
                client.sendMessage("(Privado) " + this.username + ": " + message);
                sendMessage("(Mensaje enviado a " + targetUser + "): " + message); // Confirmación
                return;
            }
        }

        sendMessage("Error: Usuario '" + targetUser + "' no encontrado.");
    }

    private void broadcastMessage(String message, ClientHandler exclude) {
        for (ClientHandler client : clients) {
            if (client != exclude) {
                try {
                    client.sendMessage(message);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

     // envia mensaje solo a este cliente
    public void sendMessage(String message) throws IOException {
        output.writeUTF(message);
    }
}