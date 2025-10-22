package org.example;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class GestorTexto {

    public ArrayList<RegistroEmpleado> leerCSV(String ruta) throws IOException, Exception {
        ArrayList<RegistroEmpleado> registros = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(ruta))) {

            reader.readLine();

            String linea;
            int numLinea = 2;

            while ((linea = reader.readLine()) != null) {
                String[] campos = linea.split(",");

                if (campos.length == 5) {
                    String matricula = campos[0];
                    String fecha = campos[1];
                    double salario = Double.parseDouble(campos[2]);
                    int sector = Integer.parseInt(campos[3]);
                    String plaza = campos[4];

                    if (!validarMatricula(matricula)) {
                        throw new Exception("Error en línea " + numLinea + ": Matrícula '" + matricula + "' no cumple el formato LDDDD.");
                    }

                    registros.add(new RegistroEmpleado(matricula, fecha, salario, sector, plaza));
                }
                numLinea++;
            }
        }
        return registros;
    }

    public void escribirCSV(ArrayList<RegistroEmpleado> registros, String rutaDestino) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(rutaDestino))) {

            writer.write("matricula,fecha de nacimiento,salario,sector,plaza\n");

            for (RegistroEmpleado reg : registros) {
                writer.write(reg.toString() + "\n");
            }
        }
    }

    private boolean validarMatricula(String matricula) {
        return matricula != null && matricula.matches("[A-Za-z]\\d{4}");
    }
}