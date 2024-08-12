import 'package:flutter/material.dart';

class CustomAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String titleText;
  final Color? backgroundColor;
  final TextStyle titleStyle;

  CustomAppBar({
    required this.titleText,
    this.backgroundColor,
    this.titleStyle = const TextStyle(
      fontSize: 20.0,
      fontWeight: FontWeight.bold,
      color: Colors.deepPurpleAccent,
    ),
  });

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: Center(
        child: Text(
          titleText,
          style: titleStyle,
        ),
      ),
      // backgroundColor: backgroundColor ??
      //     Theme.of(context)
      //         .primaryColor, // Defaults to the theme's primary color
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);
}
