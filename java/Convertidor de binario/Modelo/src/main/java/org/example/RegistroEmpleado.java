package org.example;

public class RegistroEmpleado {
    private String matricula;
    private String fechaNacimiento;
    private double salario;
    private int sector;
    private String plaza;

    public RegistroEmpleado(String matricula, String fechaNacimiento, double salario, int sector, String plaza) {
        this.matricula = matricula;
        this.fechaNacimiento = fechaNacimiento;
        this.salario = salario;
        this.sector = sector;
        this.plaza = plaza;
    }

    public String getMatricula() {
        return matricula;
    }

    public String getFechaNacimiento() {
        return fechaNacimiento;
    }

    public double getSalario() {
        return salario;
    }

    public int getSector() {
        return sector;
    }

    public String getPlaza() {
        return plaza;
    }

    @Override
    public String toString() {
        return String.format("%s,%s,%.2f,%d,%s",
                matricula, fechaNacimiento, salario, sector, plaza);
    }
}