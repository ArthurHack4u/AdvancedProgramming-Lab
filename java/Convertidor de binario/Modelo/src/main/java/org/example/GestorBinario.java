package org.example;
import java.io.*;
import java.util.ArrayList;

public class GestorBinario {

    public void escribirBinario(ArrayList<RegistroEmpleado> registros, String rutaDestino) throws IOException {
        try (DataOutputStream dos = new DataOutputStream(new FileOutputStream(rutaDestino))) {

            for (RegistroEmpleado reg : registros) {
                dos.writeUTF(reg.getMatricula());
                dos.writeUTF(reg.getFechaNacimiento());
                dos.writeDouble(reg.getSalario());
                dos.writeInt(reg.getSector());
                dos.writeUTF(reg.getPlaza());
            }
        }
    }

    public ArrayList<RegistroEmpleado> leerBinario(String ruta) throws IOException {
        ArrayList<RegistroEmpleado> registros = new ArrayList<>();

        try (DataInputStream dis = new DataInputStream(new FileInputStream(ruta))) {

            while (true) {
                String matricula = dis.readUTF();
                String fecha = dis.readUTF();
                double salario = dis.readDouble();
                int sector = dis.readInt();
                String plaza = dis.readUTF();

                registros.add(new RegistroEmpleado(matricula, fecha, salario, sector, plaza));
            }
        } catch (EOFException e) {
        }

        return registros;
    }
}