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
        sendMessage("Conectado! Eres: " + this.username);

        // Mensaje de ayuda /list
        sendMessage("Comandos disponibles: /nick <nuevo_nombre> | /pm <usuario> <mensaje> | /list");
    
        System.out.println("[CONEXIÓN] " + this.username + " se ha unido. Total: " + clients.size() + " usuarios.");
        
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
                } else if (mensajeCliente.equals("/list")) {

                    // Enviar lista de usuarios
                    sendUserList();
                } else if ("salir".equalsIgnoreCase(mensajeCliente)) {
                    break;
                } else {
                // mensaje global
                
                    String fullMessage = this.username + ": " + mensajeCliente;
                    // Calcula a cuántos les llegará
                    int recipientCount = clients.size();
                    System.out.println("[GLOBAL] " + fullMessage + " (Enviado a " + recipientCount + " usuarios)");
                    
                    broadcastMessage(fullMessage, null);
                }
            }

        } catch (IOException e) {
            System.out.println(this.username + " se ha desconectado.");
        } finally {
            clients.remove(this);
            
            System.out.println("[DESCONEXIÓN] " + this.username + " ha salido. Quedan: " + clients.size() + " usuarios.");
            
            broadcastMessage(this.username + " ha salido del chat.", this);
            try {
                clientSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void changeUserName(String command) throws IOException {
        String newNick = command.substring(6).trim();
        if (newNick.isEmpty()) {
            sendMessage("Error: El nombre no puede estar vacío.");
            return;
        }

        String oldNick = this.username;
        this.username = newNick;
        
        System.out.println("[NICK] " + oldNick + " ahora es " + this.username);
        
        sendMessage("Tu nombre ha sido cambiado a: " + this.username);
        broadcastMessage(oldNick + " ahora es conocido como " + this.username, this);
    }

    private void sendPrivateMessage(String command) throws IOException {
        String[] parts = command.split(" ", 3);
        if (parts.length < 3) {
            sendMessage("Error: Uso incorrecto. /pm <usuario> <mensaje>");
            return;
        }

        String targetUser = parts[1];
        String message = parts[2];
        for (ClientHandler client : clients) {
            if (client.username.equals(targetUser)) {
                client.sendMessage("(Privado) " + this.username + ": " + message);
                sendMessage("(Mensaje enviado a " + targetUser + "): " + message);
                
                System.out.println("[PRIVADO] " + this.username + " -> " + targetUser + ": " + message);
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

    public void sendMessage(String message) throws IOException {
        output.writeUTF(message);
    }

    // Recopila todos los nombres de usuario conectados y se los envía en un mensaje privado a este cliente.
    private void sendUserList() throws IOException {

        System.out.println("[INFO] Enviando lista de usuarios a: " + this.username);
        
        StringBuilder userList = new StringBuilder();
        userList.append("--- Usuarios Conectados (" + clients.size() + ") ---\n");
        for (ClientHandler client : clients) {
            userList.append(" * " + client.username + "\n");
        }
        userList.append("-----------------------------------");
        sendMessage(userList.toString());
    }
}