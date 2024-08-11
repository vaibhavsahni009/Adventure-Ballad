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
// w
Widget fullWidthButton({
  required String text,
  required VoidCallback onPressed,
  bool isDisabled = false, // Optional parameter to control the button state
}) {
  return ElevatedButton(
    onPressed:
        isDisabled ? null : onPressed, // Disable button if isDisabled is true
    child: Text(text),
    style: ElevatedButton.styleFrom(
      minimumSize: Size(double.infinity, 50), // Full width
      backgroundColor:
          isDisabled ? Colors.grey : Colors.white, // Change color if disabled
    ),
  );
}
