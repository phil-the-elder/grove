# Resources

All images that Grove needs to render are stored in the Resources folder. Character and item animation are controlled by a cycling algorithm that processes pngs in a code-defined order, making proper naming conventions essential to maintain proper functionality:

| Characters and Creatures |
| :--- |
| [name of creature][direction letter (s, n, e, w)][sequence number].png |
| [name of creature][direction letter (s, n, e, w)][action name][sequence number].png (for any actions taken by creature or character) |

| Items |
| :--- |
| [name of item][sequence number].png |
| [name of item]_inv.png (the image for the item inside the inventory screen) |
