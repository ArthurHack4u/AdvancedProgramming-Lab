// Archivo: MonitorEjemplo.java
import java.util.LinkedList;
import java.util.Queue;

class Buffer {
    private final Queue<Integer> lista = new LinkedList<>();
    private final int capacidad;

    public Buffer(int capacidad) {
        this.capacidad = capacidad;
    }

    public synchronized void producir(int elemento) throws InterruptedException {
        // Mientras el búfer esté lleno, el productor debe esperar.
        while (lista.size() == capacidad) {
            System.out.println("Buffer lleno. El productor está esperando...");
            wait();
        }
        
        lista.add(elemento);
        System.out.println("Productor produjo: " + elemento + " [Tamaño actual: " + lista.size() + "]");
        
        // Notifica a todos los hilos en espera (consumidores) que hay un nuevo elemento.
        notifyAll();
    }

    public synchronized int consumir() throws InterruptedException {
        // Mientras el búfer esté vacío, el consumidor debe esperar.
        while (lista.isEmpty()) {
            System.out.println("Buffer vacío. El consumidor está esperando...");
            wait();
        }
        
        int elemento = lista.poll();
        System.out.println("Consumidor consumió: " + elemento + " [Tamaño actual: " + lista.size() + "]");
        
        // Notifica a todos los hilos en espera (productores) que hay espacio disponible.
        notifyAll();
        
        return elemento;
    }
}

class Productor implements Runnable {
    private final Buffer buffer;

    public Productor(Buffer buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() {
        try {
            for (int i = 0; i < 10; i++) {
                buffer.producir(i);
                Thread.sleep(100);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

class Consumidor implements Runnable {
    private final Buffer buffer;

    public Consumidor(Buffer buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() {
        try {
            for (int i = 0; i < 10; i++) {
                buffer.consumir();
                Thread.sleep(250);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

public class ConcurrenciaMonitor {
    public static void main(String[] args) {
        // Buffer con capacidad para 5 elementos.
        Buffer buffer = new Buffer(5);
        
        System.out.println("Iniciando productor y consumidor con un buffer de capacidad 5...");

        Thread productorThread = new Thread(new Productor(buffer));
        Thread consumidorThread = new Thread(new Consumidor(buffer));

        productorThread.start();
        consumidorThread.start();
    }
}