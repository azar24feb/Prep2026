package org.example;

public class TreeTester{
    public static void main(String[] args) {
        Node root = new Node(1);
        root.left = new Node(2);
        root.left.left = new Node(4);
        root.left.right = new Node(5);
        root.left.right.left = new Node(7);
        root.left.right.right = new Node(8);
        root.right = new Node(3);
        root.right.right = new Node(6);

        Node.levelOrderTraversalWithQueue(root);
    }
}
