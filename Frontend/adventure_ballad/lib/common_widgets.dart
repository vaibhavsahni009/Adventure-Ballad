import 'package:flutter/material.dart';

/// A reusable TextField with label and border
Widget customTextField(
    {required TextEditingController controller, required String label}) {
  return LayoutBuilder(
    builder: (context, constraints) {
      double width = constraints.maxWidth * 0.5; // 50% of the available width
      return Container(
        width: width,
        child: TextField(
          controller: controller,
          decoration: InputDecoration(
            labelText: label,
            border: OutlineInputBorder(),
          ),
        ),
      );
    },
  );
}

/// A reusable ElevatedButton with full width
// w
Widget fullWidthButton({
  required String text,
  required VoidCallback onPressed,
  bool isDisabled = false, // Optional parameter to control the button state
}) {
  return Center(
    child: LayoutBuilder(
      builder: (context, constraints) {
        return ElevatedButton(
          onPressed: isDisabled
              ? null
              : onPressed, // Disable button if isDisabled is true
          child: Text(
            text,
            style: TextStyle(
              fontWeight: FontWeight.bold, // Make text bold
              fontSize: 16, // Adjust the font size if needed
            ),
          ),
          style: ElevatedButton.styleFrom(
            minimumSize:
                Size(constraints.maxWidth * 0.5, 60), // 50% of screen width
            backgroundColor: isDisabled
                ? Colors.grey
                : Colors.white, // Change color if disabled
          ),
        );
      },
    ),
  );
}

Widget fullWidthButtonWithImage({
  required String text,
  required VoidCallback onPressed,
  required String imagePath, // Path to the image
  bool isDisabled = false, // Optional parameter to control the button state
}) {
  return Center(
    child: LayoutBuilder(
      builder: (context, constraints) {
        return ElevatedButton(
          onPressed: isDisabled
              ? null
              : onPressed, // Disable button if isDisabled is true
          style: ElevatedButton.styleFrom(
            minimumSize:
                Size(constraints.maxWidth * 0.5, 60), // 50% of screen width
            backgroundColor: isDisabled
                ? Colors.grey
                : Colors.white, // Change color if disabled
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ClipOval(
                child: Image.asset(
                  imagePath,
                  height: 40, // Circular image size
                  width: 40, // Circular image size
                  fit: BoxFit.cover, // Ensure image covers the circular area
                ),
              ),
              SizedBox(
                width: constraints.maxWidth * 0.1, // 10% of screen width
              ),
              Text(
                text,
                style: TextStyle(
                  fontWeight: FontWeight.bold, // Make text bold
                  fontSize: 16, // Adjust the font size if needed
                ),
              ),
            ],
          ),
        );
      },
    ),
  );
}
