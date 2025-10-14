package org.example;

import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Connection;

public class Main {

    // --- DATOS DEL SERVIDOR SSH ---
    private static final String SSH_HOST = "fi.jcaguilar.dev";
    private static final String SSH_USER = "patito";
    private static final String SSH_PASSWORD = "cuack";
    private static final int SSH_PORT = 22;

    // --- DATOS DE LA BASE DE DATOS MARIADB ---
    private static final String DB_HOST = "localhost";
    private static final int DB_PORT = 3306;

    // --- DATOS DE ACCESO A LA BASE DE DATOS ---
    private static final String DB_USER = "becario";
    private static final String DB_PASSWORD = "FdI-its-5a";
    private static final String DB_NAME = "its5a";

    private static Session sshSession;
    private static Connection dbConnection;

    /**
     * Obtiene una conexión a la base de datos.
     * Si la conexión no existe o está cerrada, crea un nuevo túnel SSH
     * y una nueva conexión a la base de datos. La estructura interna
     */
    public static Connection getConnection() throws Exception {
        // Si la conexión ya está activa y es válida, la devolvemos para ser más eficientes.
        if (dbConnection != null && !dbConnection.isClosed()) {
            return dbConnection;
        }

        // Si la conexión no es válida, procedemos a crear una nueva desde cero.
        try {
            // Aseguramos que cualquier sesión SSH anterior esté cerrada.
            if (sshSession != null && sshSession.isConnected()) {
                sshSession.disconnect();
            }

            JSch jsch = new JSch();

            System.out.println("Estableciendo conexión SSH con " + SSH_USER + "@" + SSH_HOST + "...");
            sshSession = jsch.getSession(SSH_USER, SSH_HOST, SSH_PORT);
            sshSession.setPassword(SSH_PASSWORD);

            // Desactivar la verificación de clave de host estricta
            sshSession.setConfig("StrictHostKeyChecking", "no");

            sshSession.connect();
            System.out.println("Conexión SSH establecida.");

            // Redirigir un puerto local al puerto de la base de datos remota
            int assignedPort = sshSession.setPortForwardingL(0, DB_HOST, DB_PORT);
            System.out.println("Túnel SSH creado en localhost:" + assignedPort);

            // Cadena de conexión usando el puerto local asignado
            String conString = "jdbc:mariadb://localhost:" + assignedPort + "/" + DB_NAME;

            System.out.println("Conectando a la base de datos...");
            dbConnection = DriverManager.getConnection(conString, DB_USER, DB_PASSWORD);
            System.out.println("¡Conexión a la base de datos exitosa!");

        } catch (Exception e) {
            System.err.println("Error de conexión: " + e.getMessage());
            // Si algo falla, checamos q cierre
            closeConnection();
            throw e;
        }

        return dbConnection;
    }

    /**
     * Cierra la conexión a la base de datos y la sesión SSH.
     * Debe llamarse al cerrar la aplicación.
     */
    public static void closeConnection() {
        try {
            if (dbConnection != null && !dbConnection.isClosed()) {
                dbConnection.close();
                System.out.println("Conexión a la DB cerrada.");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            if (sshSession != null && sshSession.isConnected()) {
                sshSession.disconnect();
                System.out.println("Conexión SSH cerrada.");
            }
        }
    }
}

