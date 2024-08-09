import 'package:flutter/material.dart';

/// A reusable TextField with label and border
Widget customTextField(
    {required TextEditingController controller, required String label}) {
  return TextField(
    controller: controller,
    decoration: InputDecoration(
      labelText: label,
      border: OutlineInputBorder(),
    ),
  );
}

/// A reusable ElevatedButton with full width
Widget fullWidthButton(
    {required String text, required VoidCallback onPressed}) {
  return ElevatedButton(
    onPressed: onPressed,
    child: Text(text),
    style: ElevatedButton.styleFrom(
      minimumSize: Size(double.infinity, 50),
    ),
  );
}
