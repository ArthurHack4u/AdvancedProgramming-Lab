package org.example;

import org.example.GestorBinario;
import org.example.GestorTexto;
import org.example.RegistroEmpleado;
import org.example.VentanaPrincipal;

import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.ArrayList;

public class Controlador implements ActionListener {

    private VentanaPrincipal vista;
    private GestorTexto gestorTexto;
    private GestorBinario gestorBinario;

    public Controlador(VentanaPrincipal vista, GestorTexto gestorTexto, GestorBinario gestorBinario) {
        this.vista = vista;
        this.gestorTexto = gestorTexto;
        this.gestorBinario = gestorBinario;

        this.vista.getBtnAbrirBinario().addActionListener(this);
        this.vista.getBtnCsvABinario().addActionListener(this);
        this.vista.getBtnBinACsv().addActionListener(this); // NUEVO
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == vista.getBtnAbrirBinario()) {
            abrirBinarioEnVentana();
        } else if (e.getSource() == vista.getBtnCsvABinario()) {
            convertirCsvABinario();
        } else if (e.getSource() == vista.getBtnBinACsv()) { // NUEVO
            convertirBinACsv();
        }
    }

    private void abrirBinarioEnVentana() {
        JFileChooser fc = crearFileChooser("Selecciona el archivo binario (.bin)", "bin");

        if (fc.showOpenDialog(vista) == JFileChooser.APPROVE_OPTION) {
            try {
                File archivo = fc.getSelectedFile();
                ArrayList<RegistroEmpleado> registros = gestorBinario.leerBinario(archivo.getAbsolutePath());

                mostrarRegistrosEnTextArea(registros);

            } catch (Exception ex) {
                mostrarError("Error al leer archivo binario: " + ex.getMessage());
            }
        }
    }

    private void convertirCsvABinario() {
        JFileChooser fcCsv = crearFileChooser("Selecciona el archivo de texto (.csv)", "csv");

        if (fcCsv.showOpenDialog(vista) != JFileChooser.APPROVE_OPTION) return;

        try {
            File archivoCsv = fcCsv.getSelectedFile();

            // 1. Leer el CSV
            ArrayList<RegistroEmpleado> registros = gestorTexto.leerCSV(archivoCsv.getAbsolutePath());
            mostrarRegistrosEnTextArea(registros);

            // 3. Pedir dónde guardar el .bin
            JFileChooser fcBin = crearFileChooser("Guardar como archivo binario (.bin)", "bin");

            if (fcBin.showSaveDialog(vista) != JFileChooser.APPROVE_OPTION) return;

            File archivoBin = agregarExtension(fcBin.getSelectedFile(), ".bin");

            // 5. Escribir el binario
            gestorBinario.escribirBinario(registros, archivoBin.getAbsolutePath());
            mostrarMensaje("Archivo binario guardado exitosamente en:\n" + archivoBin.getName());

        } catch (Exception ex) {
            mostrarError("Error en la conversión a binario: " + ex.getMessage());
        }
    }

    private void convertirBinACsv() {
        JFileChooser fcBin = crearFileChooser("Selecciona el archivo binario (.bin)", "bin");

        if (fcBin.showOpenDialog(vista) != JFileChooser.APPROVE_OPTION) return;

        try {
            File archivoBin = fcBin.getSelectedFile();

            // 1. Leer el binario
            ArrayList<RegistroEmpleado> registros = gestorBinario.leerBinario(archivoBin.getAbsolutePath());

            // 2. Pedir dónde guardar el .csv
            JFileChooser fcCsv = crearFileChooser("Guardar como archivo de texto (.csv)", "csv");

            if (fcCsv.showSaveDialog(vista) != JFileChooser.APPROVE_OPTION) return;

            File archivoCsv = agregarExtension(fcCsv.getSelectedFile(), ".csv");

            // 4. Escribir el CSV
            gestorTexto.escribirCSV(registros, archivoCsv.getAbsolutePath());
            mostrarMensaje("Archivo CSV guardado exitosamente en:\n" + archivoCsv.getName());

        } catch (Exception ex) {
            mostrarError("Error en la conversión a CSV: " + ex.getMessage());
        }
    }

    private void mostrarRegistrosEnTextArea(ArrayList<RegistroEmpleado> registros) {
        vista.getJtaDatos().setText("");
        StringBuilder sb = new StringBuilder();
        for (RegistroEmpleado reg : registros) {
            sb.append(reg.toString()).append("\n");
        }
        vista.getJtaDatos().setText(sb.toString());
    }

    private JFileChooser crearFileChooser(String titulo, String extension) {
        JFileChooser fc = new JFileChooser();
        fc.setDialogTitle(titulo);
        fc.setFileFilter(new FileNameExtensionFilter("Archivos " + extension.toUpperCase() + " (*." + extension + ")", extension));
        return fc;
    }

    private File agregarExtension(File archivo, String extension) {
        String ruta = archivo.getAbsolutePath();
        if (!ruta.toLowerCase().endsWith(extension)) {
            return new File(ruta + extension);
        }
        return archivo;
    }

    private void mostrarError(String mensaje) {
        JOptionPane.showMessageDialog(vista, mensaje, "Error", JOptionPane.ERROR_MESSAGE);
    }

    private void mostrarMensaje(String mensaje) {
        JOptionPane.showMessageDialog(vista, mensaje, "Éxito", JOptionPane.INFORMATION_MESSAGE);
    }
}