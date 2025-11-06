import java.net.*;

public class UDPServer {
    public static void main(String[] args) {
        try {
            DatagramSocket serverSocket = new DatagramSocket(1520);
            byte[] receiveBuffer = new byte[1024];
            byte[] sendBuffer;

            

            while (true) {
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                serverSocket.receive(receivePacket);

                String receivedData = new String(receivePacket.getData(), 0, receivePacket.getLength());
                System.out.println("Data Received: " + receivedData);

                String response;

                if (receivedData.equalsIgnoreCase("STOP")) {
                    response = "STOP";
                } else {
                    response = receivedData.toUpperCase();
                }

                sendBuffer = response.getBytes();

                InetAddress clientAddress = receivePacket.getAddress();
                int clientPort = receivePacket.getPort();

                DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, clientAddress, clientPort);
                serverSocket.send(sendPacket);

                System.out.println("Data Sent: " + response);

                if (response.equals("STOP")) {
                    break;
                }
            }

            serverSocket.close();
        } catch (Exception e) {
            System.out.println("Error: " + e);
        }
    }
}
