// RPC Client Program

import java.io.*;
import java.net.*;

class clirpc {
    public static void main(String[] args) throws Exception {
        Socket soc = new Socket("localhost", 3000);
        DataInputStream dis = new DataInputStream(soc.getInputStream());
        PrintWriter pw = new PrintWriter(soc.getOutputStream(), true);
        DataInputStream kb = new DataInputStream(System.in);

        System.out.println("Client ready, type and press Enter key");

        String receiveMessage, sendMessage, temp;

        while (true) {
            System.out.println("\nEnter operation to perform (add, sub, mul, div)....");
            temp = kb.readLine();
            sendMessage = temp.toLowerCase();
            pw.println(sendMessage);

            System.out.println("Enter first parameter: ");
            sendMessage = kb.readLine();
            pw.println(sendMessage);

            System.out.println("Enter second parameter: ");
            sendMessage = kb.readLine();
            pw.println(sendMessage);

            System.out.flush();

            if ((receiveMessage = dis.readLine()) != null) {
                System.out.println(receiveMessage);
            }
        }
    }
}
