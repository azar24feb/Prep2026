package org.example;

import java.util.LinkedList;
import java.util.Queue;

public class Node {

    public int key;
    public Node left;
    public Node right;

    public Node(int key) {
        this.key = key;
    }

    public static void inOrder(Node root) {
        if (root == null) return;
        inOrder(root.left);
        System.out.println(root.key);
        inOrder(root.right);
    }

    public static void preOrder(Node root) {
        if (root == null) return;
        System.out.println(root.key);
        preOrder(root.left);
        preOrder(root.right);
    }

    public static void postOrder(Node root) {
        if (root == null) return;
        postOrder(root.left);
        postOrder(root.right);
        System.out.println(root.key);
    }

    public static int height(Node root) {
        if (root == null) return 0;
        return Integer.max(height(root.left), height(root.right)) + 1;
    }

    public static void printK(Node root, int k) {
        if (root == null) return;
        if (k == 0) System.out.println(root.key);
        printK(root.left, k - 1);
        printK(root.right, k - 1);
    }

    public static void levelOrderTraversalWithPrintK(Node root) {
        int height = height(root);
        for (int i = 0; i < height; i++) {
            printK(root, i);
        }
    }

    /**
     * Level order traversal or Breadth First Search with Queue
     */
    public static void levelOrderTraversalWithQueue(Node root) {
        if (root == null) return;
        Queue<Node> q = new LinkedList<>();
        q.add(root);
        while (!q.isEmpty()){
            Node curr = q.poll();
            System.out.println(curr.key);
            if (curr.left != null) q.add(curr.left);
            if (curr.right != null) q.add(curr.right);
        }
    }
}
